#-----------------------------------------------------------------------
# This Makefile installs M1QN3 in the Libopt environment
#-----------------------------------------------------------------------

# The full pathname of the M1QN3 directory is set by removing the string
# '/libopt' from the end of the present directory pathname

m1qn3_dir = $(PWD:/libopt=)

# Some useful directories and files

m1qn3_bin_dir = $(m1qn3_dir)/bin
m1qn3_src_dir = $(m1qn3_dir)/src
m1qn3_src     = $(m1qn3_src_dir)/m1qn3.f

# Include file

include $(LIBOPT_DIR)/platforms/make.$(LIBOPT_PLAT)

# Here is the file that is generated by this Makefile. Note that its
# name needs to be quoted by the environment variable $LIBOPT_PLAT.

libopt_m1qn3_obj = $(LIBOPT_DIR)/solvers/m1qn3/bin/m1qn3.$(LIBOPT_PLAT).o

libopt: $(libopt_m1qn3_obj)

#-----------------------------------------------------------------------

$(libopt_m1qn3_obj): $(m1qn3_bin_dir)/m1qn3.$(LIBOPT_PLAT).o
	rm -f $(libopt_m1qn3_obj)
	ln -s -f \
	   $(m1qn3_bin_dir)/m1qn3.$(LIBOPT_PLAT).o \
	   $(libopt_m1qn3_obj)

$(m1qn3_bin_dir)/m1qn3.$(LIBOPT_PLAT).o: $(m1qn3_src)
	$(F90) $(F90FLAGS) $(F90NOLD) \
	   $(m1qn3_src) \
	   -o $(m1qn3_bin_dir)/m1qn3.$(LIBOPT_PLAT).o

#-----------------------------------------------------------------------

purge:	
	rm -f \
	   $(m1qn3_bin_dir)/m1qn3.$(LIBOPT_PLAT).o \
	   $(libopt_m1qn3_obj)

